from project_generator.graph import SRSState, builder
import asyncio
async def main():
    state = SRSState()
    compiled_graph = builder.compile()
    final_state = await compiled_graph.ainvoke(state)
    print(final_state)


print("FastAPI project with PostgreSQL integration generated!")

if __name__=="__main__":
    asyncio.run(main())