import time
import azure.cognitiveservices.speech as speechsdk

def check_result(result):
    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))

# 1 . Creates an instance of a speech config
#     a. need to get the key from azure speech
#       - specified subscription key
#       - service region( see https://aka.ms/speech/sdkregion)

speech_key = 'speech_key_from_azure'
service_region = "koreacentral"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)

# 2. Creates an audio configuration that points to an audio file.
audio_filename = "/Users/1110647/projects/azure_speech_test/audio2.wav"
audio_input = speechsdk.AudioConfig(filename=audio_filename)

# 3. Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_input)


# # 4.  single utterance
# #  - listning for silence at the end of a speech
# #  - maximum of 15 seconds
# print("Recognizing single utterance...")
# result = speech_recognizer.recognize_once()
# check_result(result)


# 5. Long-running multi-utterance recognition
     # User must subscribe to events to receive recognition results.
done = False
result = False

def stop_cb(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    global done
    done = True

def return_result(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('RECOGNIZED on {}'.format(evt))
    global result
    result = evt.result

# Connect callbacks to the events fired by the speech recognizer
# speech_recognizer.recognizing.connect(
#     lambda evt: print('RECOGNIZING: {}'.format(evt)))
# speech_recognizer.session_started.connect(
#     lambda evt: print('SESSION STARTED: {}'.format(evt)))
# speech_recognizer.session_stopped.connect(
#     lambda evt: print('SESSION STOPPED {}'.format(evt)))
# speech_recognizer.canceled.connect(
#     lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events

speech_recognizer.recognized.connect(return_result)
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition
# Wait while finishes processing stt.
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(.5)

speech_recognizer.stop_continuous_recognition()
check_result(result)


