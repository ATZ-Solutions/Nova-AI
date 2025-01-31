import grpc
from riva.grpc import speech_to_text_pb2, speech_to_text_pb2_grpc
from riva.grpc import tts_pb2, tts_pb2_grpc

class RivaASRClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')  # Riva ASR service address
        self.stub = speech_to_text_pb2_grpc.SpeechToTextStub(self.channel)

    def transcribe_audio(self, audio_file):
        # Send the audio to Riva ASR for transcription
        with open(audio_file, 'rb') as f:
            audio_data = f.read()

        request = speech_to_text_pb2.RecognizeRequest(
            audio=audio_data,
            config=speech_to_text_pb2.RecognitionConfig(
                encoding=speech_to_text_pb2.RecognitionConfig.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US"
            )
        )
        response = self.stub.Recognize(request)
        return response.results[0].alternatives[0].transcript if response.results else "No speech detected"

class RivaTTSClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50052')  # Riva TTS service address
        self.stub = tts_pb2_grpc.TextToSpeechStub(self.channel)

    def synthesize_text(self, text):
        # Send text to Riva TTS for speech synthesis
        request = tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(text=text),
            voice=tts_pb2.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-D"),
            audio_config=tts_pb2.AudioConfig(audio_encoding=tts_pb2.AudioEncoding.LINEAR16)
        )
        response = self.stub.SynthesizeSpeech(request)
        # Save the resulting audio
        with open('feedback_audio.wav', 'wb') as f:
            f.write(response.audio_content)
        return 'feedback_audio.wav'
