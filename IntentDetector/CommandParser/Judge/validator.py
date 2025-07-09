# IntentDetector/CommandParser/judge/validator.py

class CommandValidator:
    """
    质检员 (Judge/Validator)。
    只负责判断指令是否合法，不关心内容如何转换。
    """

    def __init__(self):
        self.required_keys = {"plugin", "command", "args", "response"}

    def validate(self, raw_command: dict) -> tuple[bool, str]:
        """
        验证指令的合法性。
        :return: 一个元组 (是否通过, 错误信息)
        """
        # 检查1：是不是字典？
        if not isinstance(raw_command, dict):
            return False, "AI响应格式错误，不是一个有效的JSON对象。"

        # 检查2：必要的键是否都存在？
        if not self.required_keys.issubset(raw_command.keys()):
            missing_keys = self.required_keys - raw_command.keys()
            return False, f"AI响应结构不完整，缺少键: {missing_keys}"

        # 未来可以增加更多检查...

        return True, "指令通过校验"