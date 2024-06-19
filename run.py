import importlib
import example.input.data.data as data_module
import SLDGenerator as SLDGenerator_module


def main():
    importlib.reload(data_module)
    importlib.reload(SLDGenerator_module)
    
    configs = data_module.configs
    output_dir = 'example/output'
    input_dir = 'example/input'

    for config in configs:
        print(config)
        generator = SLDGenerator_module.SLDGenerator(config, output_dir,input_dir)
        generator.create_sld()

if __name__ == "__main__":
    main()
