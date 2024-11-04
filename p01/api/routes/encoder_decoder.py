import base64, re

def Decode(encoded_content):
  match = re.search(r"b'([^']*)'", encoded_content)
  if match:
      encoded_content = match.group(1)
      byte_content = base64.b64decode(encoded_content)
      content = byte_content.decode("utf-8")
      return content
  else:
     print("Error matching the pattern")
     return ""
  
def Encode(content):
    encoded_content = base64.b64encode(content.encode("utf-8"))
    return encoded_content