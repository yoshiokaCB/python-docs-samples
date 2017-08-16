#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


# [START def_transcribe_file]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START migration_sync_request]
    # [START migration_audio_config_file]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        # language_code='en-US')
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='ja-JP')
    # [END migration_audio_config_file]

    # [START migration_sync_response]
    response = client.recognize(config, audio)
    # [END migration_sync_request]
    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        # print('Transcript: {}'.format(alternative.transcript))
        # print('transcript: ', alternative.transcript)
        print(alternative.transcript)
    # [END migration_sync_response]
# [END def_transcribe_file]



# [START def_transcribe_gcs]
def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        # max_alternatives=15,
        language_code='ja-JP')
    # [END migration_audio_config_gcs]

    # operation = client.recognize(config, audio)
    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=360)

    # alternatives = result.results[0].alternatives

    for result in result.results:
        alternatives = result.alternatives
        for alternative in alternatives:
            # print('Transcript: {}'.format(alternative.transcript))
            # print('Confidence: {}'.format(alternative.confidence))
            print(alternative.transcript)
            print(alternative.confidence)

    # import pdb; pdb.set_trace()
    #
    # for alternative in alternatives:
    #     # print('Transcript: {}'.format(alternative.transcript))
    #     # print('Confidence: {}'.format(alternative.confidence))
    #     print(alternative.transcript)
    #     print(alternative.confidence)
    # response = client.recognize(config, audio)
    # alternatives = response.results[0].alternatives
    #
    # for alternative in alternatives:
    #     # print('Transcript: {}'.format(alternative.transcript))
    #     print(alternative.transcript)
# [END def_transcribe_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
