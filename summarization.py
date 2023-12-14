from transformers import pipeline

model = pipeline("summarization", model="t5-small", framework="tf")
print("---Model loaded---")

def summarize(text):
  sequences = model(text, min_length=0, max_length=text.count(" ")+1, num_return_sequences=1)
  return sequences[0]['summary_text']