def validate_file_extension(file_extension):
    allowed_extensions = ['pdf', 'dxf', 'xlsx', 'xls', 'txt', 'png', 'jpg', 'jpeg', 'rar', 'zip', 'doc', 'docx', 'igs']  
    if file_extension in allowed_extensions:
        return True
    else:
        return False

def validate_file_inquiry_extension(file_extension):
    allowed_extensions = ['zip', 'rar']  
    if file_extension in allowed_extensions:
        return True
    else:
        return False