import sys

def error_message_details(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()

    filename = exc_tb.tb_frame.f_code.co_filename
    error_msg = "Error occored in python script\nname :[{0}]\nline number :[{1}]\nerror message :[{2}]".format(
        filename,
        exc_tb.tb_lineno,
        str(error)
    )

    return error_msg

class CustomException(Exception):
    def __init__(self, error_message,error_delail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_delail)

    def __str__(self) -> str:
        return self.error_message



