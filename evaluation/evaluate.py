import argparse
import json
import os

from dotenv import load_dotenv

load_dotenv()
from ratelimit import limits, sleep_and_retry

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

import asyncio
import logging

logger = logging.getLogger(__name__)

# 每分钟最大请求数
RATE_LIMIT = 1200
# 60秒的时间窗口
TIME_PERIOD = 60

llm: ChatOpenAI


@sleep_and_retry
@limits(calls=RATE_LIMIT, period=TIME_PERIOD)
async def chat(query):
    """
    提取关键字
    :param query:
    :return:
    """
    messages = [
        HumanMessage(content=query)
    ]

    result = await llm.ainvoke(messages)
    return result.content


async def evaluate(model, eval_item, ds):
    """
    评估
    :return:
    """
    eval_result = {}

    for (i, item) in enumerate(ds):
        prompt = item['instruction'] + '\n' + item['question']
        # 增加流量控制，1rpm。
        start = asyncio.get_event_loop().time()
        try:
            predict = await chat(prompt)
        except Exception as e:
            predict = ''
            print(e)
        end = asyncio.get_event_loop().time()
        predict = {
            "origin_prompt": [
                {
                    "role": "HUMAN",
                    "prompt": prompt
                }
            ],
            "prediction": predict,
            "refr": item['answer']
        }
        print(f'{i:<4} {str(round(end - start, 2)) + "s":<6} {predict}')
        eval_result[i] = predict

    output_file = f'predictions/zero_shot/{model}/{eval_item}.json'
    # 创建目录
    json_dir = '/'.join(output_file.split('/')[:-1])
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    fw = open(output_file, 'w')
    json.dump(eval_result, fw, indent=4, ensure_ascii=False)


async def main():
    parser = argparse.ArgumentParser(description='Evaluate LLM performance on a dataset.')
    parser.add_argument('--model', type=str, required=True, help='Model name')
    parser.add_argument('--eval_item', type=str, required=True, help='Evaluation item identifier')

    args = parser.parse_args()

    model = args.model
    eval_item = args.eval_item

    ds_test_file = f'data/zero_shot/{eval_item}.json'
    ds_test = json.load(open(ds_test_file))
    print(f'length of ds_test: {len(ds_test)}')

    global llm
    llm = ChatOpenAI(
        model=model,
        temperature=0,
        streaming=False,
        request_timeout=60,
        max_retries=1,
    )
    await evaluate(model, eval_item, ds_test)


if __name__ == '__main__':
    asyncio.run(main())
