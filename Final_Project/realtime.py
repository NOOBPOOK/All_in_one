import streamlit as st
import websockets
import asyncio
import base64
import json
import pyaudio
import os
from pathlib import Path

# Session state
if 'text' not in st.session_state:
	st.session_state['text'] = 'Listening...'
	st.session_state['run'] = False

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# Open an audio stream with above parameter settings
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# Start/stop audio transmission
def start_listening():
	st.session_state['run'] = True

def stop_listening():
	st.session_state['run'] = False

st.image("logo.png",width=200)
# Web user interface
st.title('🎙️ Real-Time NOOBPOOK Transcription App')

col1, col2 = st.columns(2)

col1.button('Start', on_click=start_listening)
col2.button('Stop', on_click=stop_listening)

# Send audio (Input) / Receive transcription (Output)
async def send_receive():
	URL = f"wss://api-inference.huggingface.co/bulk/stream/cpu/facebook/bart-large-mnli"

	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(URL) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving messages ...")

		#session_begins = await _ws.recv()
		#print(session_begins)
		print("Sending messages ...")
	
		async def send():
			while st.session_state['run']:
				try:
					API_TOKEN = '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'
					data = stream.read(FRAMES_PER_BUFFER)
					data = base64.b64encode(data).decode("utf-8")
					json_data = json.dumps({"audio_data":str(data)})
					await _ws.send(f"Bearer {API_TOKEN}".encode("utf-8"))
					r = await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"

				r = await asyncio.sleep(0.01)


		async def receive():
			og = []
			while st.session_state['run']:
				try:
					result_str = await _ws.recv()
					result = json.loads(result_str)
					if result['type'] == "results":
						og.append(result["outputs"])
						print(og)
						st.session_state['text'] = result
						st.write(st.session_state['text'])

					if result['type'] == "status":
						st.write(result['message'])
						break

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"
			
		send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())
