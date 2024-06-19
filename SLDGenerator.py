import xml.etree.ElementTree as ET
import os
import base64
from PIL import Image
import importlib
from io import BytesIO


class SLDGenerator:
    def __init__(self, config, output_dir='output', input_dir='input'):
        self.config = config
        self.output_dir = output_dir
        self.input_dir = input_dir
        self.img_dir_path = input_dir+'/img'
        print(self.config)
        print(self.output_dir)
        print(self.input_dir)
        print(self.img_dir_path)
        self.layer_name = config['layer_name']
        self.dir = config.get('dir', '')
        self.conf_rules = config.get('rules',[])

        ET.register_namespace("", "http://www.opengis.net/sld")
        ET.register_namespace("se", "http://www.opengis.net/se")
        ET.register_namespace("ogc", "http://www.opengis.net/ogc")
        ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def resize_image(self, image_path, size=10):
        with Image.open(image_path) as img:
            
            resized_img = img.resize((size, size))
            return resized_img

    def image_to_base64(self, image):
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def update_config_with_base64(self, name, config):
        image_path = os.path.join(f"{self.img_dir_path}/{self.dir}", f"{name}.png")
        print('aaaaaaa----')
        print(image_path)
        size = int(config['size'])
        print(size)
        resized_image = self.resize_image(image_path, size)
        base64_str = self.image_to_base64(resized_image)
        return base64_str

    def create_symbolizer(self, type, name, conf):
        stroke_data = conf.get('stroke')
        fill_data = conf.get('fill')
        slash_data = conf.get('slash')

        if type == 'polygon' or type == 'polygon_slash':
            el_symbolizer = ET.Element("se:PolygonSymbolizer")
            fill = ET.SubElement(el_symbolizer, "se:Fill")
            if type == 'polygon':
                css_param = ET.SubElement(fill, "se:SvgParameter", attrib={"name": "fill"})
                css_param.text = fill_data['text']
            elif type == 'polygon_slash':
                graphic_fill = ET.SubElement(fill, "se:GraphicFill")
                graphic = ET.SubElement(graphic_fill, "se:Graphic")
                mark = ET.SubElement(graphic, "se:Mark")
                well_known_name = ET.SubElement(mark, "se:WellKnownName")
                well_known_name.text = 'shape://' + slash_data['shape']
                stroke = ET.SubElement(mark, "se:Stroke")
                css_param_stroke = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke"})
                css_param_stroke.text = fill_data['text']
                css_param_stroke_width = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke-width"})
                css_param_stroke_width.text = slash_data.get('width', '1')
                size = ET.SubElement(graphic, "se:Size")
                size.text = "16"

            if stroke_data:
                stroke = ET.SubElement(el_symbolizer, "se:Stroke")
                css_param_stroke = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke"})
                css_param_stroke.text = stroke_data['text']
                css_param_stroke_width = ET.SubElement(css_param_stroke, "se:SvgParameter", attrib={"name": "stroke-width"})
                css_param_stroke_width.text = stroke_data['width']

        elif type == 'line':
            el_symbolizer = ET.Element("se:LineSymbolizer")
            if stroke_data:
                stroke = ET.SubElement(el_symbolizer, "se:Stroke")
                css_param_stroke = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke"})
                css_param_stroke.text = stroke_data['text']
                css_param_stroke_width = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke-width"})
                css_param_stroke_width.text = stroke_data['width']
                css_param_stroke_linejoin = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke-linejoin"})
                css_param_stroke_linejoin.text = 'bevel'
                css_param_stroke_linecap = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke-linecap"})
                css_param_stroke_linecap.text = 'square'
                if stroke_data.get('dasharray'):
                    css_param_stroke_dasharray = ET.SubElement(stroke, "se:SvgParameter", attrib={"name": "stroke-dasharray"})
                    css_param_stroke_dasharray.text = stroke_data['dasharray']

        elif type == 'point':
            print(1)
            
            base64_data = self.update_config_with_base64(name, conf)
            el_symbolizer = ET.Element("se:PointSymbolizer")
            graphic = ET.SubElement(el_symbolizer, "se:Graphic")
            external_graphic = ET.SubElement(graphic, "se:ExternalGraphic")
            inline_content = ET.SubElement(external_graphic, "se:InlineContent", attrib={"encoding": "base64"})
            inline_content.text = base64_data
            format_elem = ET.SubElement(external_graphic, "se:Format")
            format_elem.text = 'image/png'

        return el_symbolizer

    def create_filter(self, conf):
        el_filter = ET.Element("ogc:Filter", attrib={"xmlns:ogc": "http://www.opengis.net/ogc"})
        property_is_equal_to = ET.SubElement(el_filter, "ogc:PropertyIsEqualTo")
        property_name = ET.SubElement(property_is_equal_to, "ogc:PropertyName")
        property_name.text = conf.get('name', '')
        literal = ET.SubElement(property_is_equal_to, "ogc:Literal")
        literal.text = conf.get('value', '')
        return el_filter

    def create_rule(self, conf):
        conf_name = conf.get('name', '')
        conf_type = conf.get('type', '')
        conf_symbolizer = conf.get('symbolizer', {})
        conf_filter = conf.get('filter')

        rule = ET.Element("se:Rule")
        rule_name = ET.SubElement(rule, "se:Name")
        rule_name.text = conf_name

        # desc
        description = ET.SubElement(rule, "se:Description")
        title = ET.SubElement(description, "se:Title")
        title.text = conf_name

        # filter
        if conf_filter:
            el_filter = self.create_filter(conf_filter)
            rule.append(el_filter)

        # symbolizer
        if isinstance(conf_symbolizer, list):
            for conf_symbolizer_item in conf_symbolizer:
                el_symbolizer = self.create_symbolizer(conf_type, conf_name, conf_symbolizer_item)
                rule.append(el_symbolizer)
        else:
            el_symbolizer = self.create_symbolizer(conf_type, conf_name, conf_symbolizer)
            rule.append(el_symbolizer)

        return rule

    def create_sld(self):
        print('SLDGenerator.create_sld-----------')
        sld = ET.Element("StyledLayerDescriptor", 
                        attrib={"version": "1.1.0", 
                                "xsi:schemaLocation": "http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd",
                                "xmlns": "http://www.opengis.net/sld",
                                "xmlns:se": "http://www.opengis.net/se",
                                "xmlns:ogc": "http://www.opengis.net/ogc",
                                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})

        # Layer Name
        named_layer = ET.SubElement(sld, "NamedLayer")
        name = ET.SubElement(named_layer, "se:Name")
        name.text = self.layer_name

        # User Style
        user_style = ET.SubElement(named_layer, "UserStyle")
        style_name = ET.SubElement(user_style, "se:Name")
        style_name.text = self.layer_name

        # Feature Type Style
        feature_type_style = ET.SubElement(user_style, "se:FeatureTypeStyle")

        # Rules
        print(self.conf_rules)
        for conf_rule in self.conf_rules:
            el_rule = self.create_rule(conf_rule)
            feature_type_style.append(el_rule)


        # Create directory if it doesn't exist
        dir_path = os.path.join(self.output_dir, self.dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, f"{self.layer_name}.sld")
        print(f"SLD file created at: {file_path}")

        tree = ET.ElementTree(sld)
        tree.write(file_path, xml_declaration=True, encoding='utf-8', method="xml")



