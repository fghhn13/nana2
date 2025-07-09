# IntentDetector/CommandParser/translate/formatter.py

class CommandFormatter:
    """
    翻译/格式化员 (Translate/Formatter)。
    负责将通过验证的指令进行最终的标准化处理。
    """

    def format(self, valid_command: dict) -> dict:
        """
        目前我们的AI已经能输出标准格式，所以这里暂时只做“透传”。
        但未来如果AI格式有变，所有的转换逻辑都在这里实现，而不用修改别的地方。
        """
        # 例如，未来可以做这样的转换：
        # if 'action' in valid_command:
        #     valid_command['command'] = valid_command.pop('action')

        # 目前，我们直接返回，相信它已经是标准格式了。
        return valid_command