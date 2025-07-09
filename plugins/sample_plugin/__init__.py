from plugins.base_plugin import BasePlugin

class SamplePlugin(BasePlugin):
    def get_name(self):
        return "sample_plugin"

    def get_commands(self):
        return ["do"]

    def execute(self, command, args, controller):
        pass


def get_plugin():
    return SamplePlugin()
