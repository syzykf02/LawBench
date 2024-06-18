import json


def convert_format_1(input_file, output_file):
    fr = open(input_file, 'r')
    fw = open(output_file, 'w')
    for line in fr:
        data = json.loads(line)
        messages = {
            "messages": [{
                "role": "user",
                "content": data['input']
            }, {
                "role": "assistant",
                "content": data['output']
            }]
        }
        fw.write(json.dumps(messages, ensure_ascii=False) + '\n')
    fw.close()


def convert_format_2(input_file, output_file):
    fr = open(input_file, 'r')
    fw = open(output_file, 'w')
    for line in fr:
        data = json.loads(line)
        messages = {
            "messages": [{
                "role": "user",
                "content": data['input']
            }, {
                "role": "assistant",
                "content": data['output'] + '\n法律依据：\n' + '\n'.join(data['reference'])
            }]
        }
        fw.write(json.dumps(messages, ensure_ascii=False) + '\n')
    fw.close()


if __name__ == '__main__':
    # input_file = '/Users/zhangx/git2/DISC-Law-SFT/DISC-Law-SFT-Pair.jsonl'
    # output_file = '/Users/zhangx/git2/DISC-Law-SFT/DISC-Law-SFT-Pair2.jsonl'
    # convert_format_1(input_file, output_file)

    input_file = '/Users/zhangx/git2/DISC-Law-SFT/DISC-Law-SFT-Triplet-released.jsonl'
    output_file = '/Users/zhangx/git2/DISC-Law-SFT/DISC-Law-SFT-Triplet-released2.jsonl'
    convert_format_2(input_file, output_file)
