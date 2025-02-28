from crew import CrewAI

if __name__ == "__main__":
    crew_instance = CrewAI()

    print("🧠 Testing Data Assistant...")
    response = crew_instance.data_agent()("What were the total sales last month?")
    print("\n📝 AI Response:\n", response)

    print("\n📊 Testing BI Analyst...")
    response = crew_instance.bi_agent()(
        "What are the key sales trends for this quarter?"
    )
    print("\n📊 AI Insights:\n", response)
