import hashlib
def construct_offline_player_uuid(username):
    #extracted from the java code:
    #new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));

    def add_uuid_stripes(string):
        string_striped = (
            string[:8] + '-' +
            string[8:12] + '-' +
            string[12:16] + '-' +
            string[16:20] + '-' +
            string[20:]
        )
        return string_striped

    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    #set the version to 3 -> Name based md5 hash
    byte_array[6] = hash[6] & 0x0f | 0x30
    #IETF variant
    byte_array[8] = hash[8] & 0x3f | 0x80

    hash_modified = bytes(byte_array)
    offline_player_uuid = add_uuid_stripes(hash_modified.hex())

    return offline_player_uuid

print(construct_offline_player_uuid('Francisco5386'))

exit()
import speech_recognition
import pyttsx3

recognizer = speech_recognition.Recognizer()

while False:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio, language="es-ESe")
            text = text.lower()

            print(f"\n-- {text}\n")
    
    except Exception as ex:
        print(f"{type(ex)}, {ex}, {ex.args}")
        recognizer = speech_recognition.Recognizer()
        continue


import argparse

import inspect

def myfun(mode, count=1, frobify=False, *files):
    print('Doing %s %d times on %s (%sfrobifying)' % (
        mode, count, files, '' if frobify else 'not '
    ))

def funopt(fun, argv=None):
    parser = argparse.ArgumentParser()

    if hasattr(inspect, 'getfullargspec'):
        spec = inspect.getfullargspec(fun)
    else:
        spec = inspect.getargspec(fun)

    num_defaults = len(spec.defaults) if spec.defaults is not None else 0




    for i in range(len(spec.args)):
        if i < len(spec.args) - num_defaults:
            parser.add_argument(spec.args[i])
        elif spec.defaults[i - len(spec.args)] is False:
            parser.add_argument('--' + spec.args[i], 
                                default=False, action='store_true')
        else:
            default = spec.defaults[i - len(spec.args)]
            parser.add_argument('--' + spec.args[i],
                                default=default,
                                type=type(default))
    if spec.varargs is not None:
            parser.add_argument(spec.varargs,
                                nargs='*')

    kwargs = vars(parser.parse_args(argv))
    args = []
    for arg in spec.args:
        args += [kwargs[arg]]
    if spec.varargs is not None:
        args += kwargs[spec.varargs]

    fun(*args)


funopt(myfun)