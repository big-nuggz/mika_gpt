import tiktoken


def get_token_count_from_string(text: str, encoder: tiktoken.Encoding) -> int:
    '''
    self explanatory
    '''
    return len(encoder.encode(text))

def get_token_count_from_chat(chat: dict, encoder: tiktoken.Encoding, estimate_image_token=True) -> int:
    '''
    returns token count of entire chat

    image tokens are estimated with max token of gpt-4.1 (1536)
    '''
    tokens = 0
    for message in chat:
        for key, value in message.items():
            if type(value) == str:
                tokens += get_token_count_from_string(value, encoder)
            
            elif key == 'content':
                for content in value:
                    for c_key, c_value in content.items():
                        if c_key == 'text':
                            tokens += get_token_count_from_string(c_value, encoder)
                        elif (c_key == 'image_url') and estimate_image_token:
                            tokens += 1536
                    
    tokens += 3 # they have 3 extra tokens for some reasons, apparently

    return tokens


if __name__ == '__main__':
    # from constants import MODEL_NON_VISION
    # ENCODING = tiktoken.encoding_for_model(MODEL_NON_VISION)
    token_encoding = tiktoken.encoding_for_model('gpt-4o')
    print(token_encoding)

    test_string = 'hello this is a test encoding of a random text that I just wrote down super quick'

    print(get_token_count_from_string(test_string, token_encoding))

    chat_id = 'df6009f0-315a-4c18-b227-423fbd6197bf'
    
    from file import load_json

    chat_file = load_json(f'chats/{chat_id}.json')
    print(get_token_count_from_chat(chat_file['current_conversation'], token_encoding))