import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent  # 1. 修改导入
from langchain_core.prompts import ChatPromptTemplate

from agent.tools.redis_tool import redis_health_check
from agent.tools.mysql_tool import mysql_health_check
from agent.tools.nginx_tool import nginx_health_check

load_dotenv()

def build_agent():
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        temperature=0
    )

    tools = [redis_health_check, mysql_health_check, nginx_health_check]

    # 2. 使用 create_agent 构建 Agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""你是中间件运维专家，负责巡检 Redis、MySQL、Nginx。
你可以调用工具获取实时状态，然后给出：
1. 健康状态总结
2. 发现的风险项
3. 调优建议
""",
        # 3. 在新版中，ReAct 的格式已由框架内部处理，无需手动提供 PromptTemplate
    )
    return agent

def main():
    agent = build_agent()
    print("中间件健康巡检 Agent 已启动")
    print("输入 'exit' 退出\n")
    while True:
        q = input("巡检需求 > ")
        if q.lower() == "exit":
            break
        # 4. 新版调用方式：传入 messages 列表
        result = agent.invoke({"messages": [{"role": "user", "content": q}]})
        # 5. 新版输出获取方式：取 messages 列表的最后一条
        print(f"\n巡检报告：\n{result['messages'][-1].content}\n")

if __name__ == "__main__":
    main()
