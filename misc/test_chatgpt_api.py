from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message.content);

