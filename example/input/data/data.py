def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}".upper()


configs = [
    # line-simple: 不需要判断字段：1个rule，一条实线
    {
    "dir":"example/line-simple",
    "layer_name": "高速铁路",
    "rules": [
        {
            "name": "高速铁路",
            "type": "line",
            # "filter": {
            #   "name": "判断的字段",
            #   "value": "判断的值",
            # },
            "symbolizer": [
                {
                "stroke": {
                    'text': rgb_to_hex(255,	0, 0),
                    'width': "1.5",
                    # "dasharray":"4 6"
                    },

            },
                
            ]
        }
    ]
    },
    # line-filter: 判断字段
    { # 需要判断字段：多个rule
   "dir":"example/line-filter",
    "layer_name": "高速铁路",
    "rules": [
        {
            "name": "一级",
            "type": "line",
            "filter": {
              "name": "类型",
              "value": "一级",
            },
            "symbolizer": [
               {
                "stroke": {
                    'text': rgb_to_hex(255,	0, 0),
                    'width': "1.1",
                    # "dasharray":"4 6"
                  },

            },
              
            ]
        },
        {
            "name": "二级",
            "type": "line",
            "filter": {
              "name": "类型",
              "value": "二级",
            },
            "symbolizer": [
               {
                "stroke": {
                    'text': rgb_to_hex(0, 0, 255),
                    'width': "1.0",
                    # "dasharray":"4 6"
                  },

            },
              
            ]
        },
    ]
},

    # line-dasharray:虚线
    # 各种各样的虚线：数重复：
# 比如 —— —— . . —— —— . .  
# 重复 —— —— . . 那么——20, 空格6, ——20, 空格6, .1, 空格6, .1, 空格6
# "dasharray":"20 6 20 6 1 6 1 6"
{
   "dir":"example/line-dasharray",
    "layer_name": "高速铁路",
    "rules": [
        {
            "name": "高速铁路",
            "type": "line",
            "symbolizer": [
               {
                "stroke": {
                    'text': rgb_to_hex(255,	0, 0),
                    'width': "1.0",
                    "dasharray":"20 6 20 6 1 6 1 6"
                  },

            },
              
            ]
        }
    ]
},
# line-multi:
{# 两条不同颜色的线：多个symbolizer，先写粗的再写细的，虚线加dasharray
   "dir":"example/line-multi",
    "layer_name": "高速铁路",
    "rules": [
        {
            "name": "高速铁路",
            "type": "line",
            "symbolizer": [
               {
                "stroke": {
                    'text': rgb_to_hex(100,	100,	100),
                    'width': "1.5",
                    # "dasharray":"4 6"
                  },

            },
               {
                "stroke": {
                    'text': rgb_to_hex(245,	245,	245),
                    'width': "1.0",
                    "dasharray":"4 6"
                  },

            },
              
            ]
        }
    ]
},

  # point-base64:
  {
  "dir":"example/point-base64",
   "layer_name": "矿山",
   "rules": [
       {
           "name": "地下水",
           "type": "point",
        #    "filter": {
        #      "name": "矿种名称",
        #      "value": "地下水",
        #    },
           "symbolizer": {
               "size":"10",
               "base64":""

           },
       }, 
        
   ],
   
},


  # polygon-nostroke:
  {
    "dir": "example/polygon-nostroke",
    "layer_name": "水库工程",
    "rules": [
        {
            "name": "大型",
            "type": "polygon",
            "symbolizer": {
                "fill": {
                    "text": rgb_to_hex(0, 87, 255)
                }
            },
        },
     
    ]
},
  # polygon-stroke:
  {
    "dir": "example/polygon-stroke",
    "layer_name": "水库工程",
    "rules": [
        {
            "name": "大型",
            "type": "polygon",
            "symbolizer": {
                "fill": {
                    "text": rgb_to_hex(0, 87, 255)
                },
                "stroke": {
                    'text': rgb_to_hex(211, 255, 0),
                    'width': "0.1"
                }
            },
        },
     
    ]
},
  # polygon-filter
  {
    "dir": "example/polygon-filter",
    "layer_name": "水库工程",
    "rules": [
        {
            "name": "大型",
            "type": "polygon",
            "filter": {
                "name": "等级",
                "value": "大型",
            },
            "symbolizer": {
                "fill": {
                    "text": rgb_to_hex(0, 87, 255)
                },
                "stroke": {
                    'text': rgb_to_hex(211, 255, 0),
                    'width': "0.1"
                }
            },
        },
        {
            "name": "中型",
            "type": "polygon",
            "filter": {
                "name": "等级",
                "value": "中型",
            },
            "symbolizer": {
                "fill": {
                    "text": rgb_to_hex(219, 247, 193)
                }
            },
        },
    ]
},
  
  # polygon-fill-slash
  # shape://vertline A vertical line (suitable for hatch fills or to make railroad symbols)
  # shape://horline  A horizontal line (suitable for hatch fills)
  # shape://slash A diagonal line leaning forwards like the “slash” keyboard symbol (suitable for diagonal hatches)
  # shape://backslash Same as shape://slash, but oriented in the opposite direction
  # shape://dot A very small circle with space around
  # shape://plus A + symbol, without space around (suitable for cross-hatch fills)
  # shape://times A “X” symbol, without space around (suitable for cross-hatch fills)

  {
    "dir": "example/polygon-fill-slash",
    "layer_name": "水库工程",
    "rules": [
        {
            "name": "大型",
            "type": "polygon_slash",
            "symbolizer": {
                "fill": {
                    "text": rgb_to_hex(255, 170, 0)
                },
                "slash":{
                  "shape":"times", 
                },
                "stroke": {
                    'text': rgb_to_hex(255, 170, 0),
                    'width': "0.35"
                }
            },
        },
    ]
},





]