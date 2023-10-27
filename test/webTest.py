import aiohttp
import asyncio

# Define the form data
data = {
    'text': '1+1'
}


# Define the async function
async def make_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.text()


# Define the main function
async def main():
    # Make the async request
    response = await make_request('http://localhost:5000/get_xinghuo', data)

    # Check the response and convert to UTF-8
    response_utf8 = response.encode('utf-8')
    print(response_utf8.decode('utf-8'))


# Run the event loop
for i in range(4):
    asyncio.run(main())

