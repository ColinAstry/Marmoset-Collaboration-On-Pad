import wave

def cut_reverse_adhere_sound(input_file, output_file):
    # Open the input sound file
    with wave.open(input_file, 'rb') as wav_in:
        # Get the parameters of the input sound
        params = wav_in.getparams()

        # Read the audio data
        frames = wav_in.readframes(params.nframes)

    # Determine the length of each part
    total_length = len(frames)
    part_length = total_length // 3

    # Cut the sound into three parts
    part1 = frames[:part_length]
    part2 = frames[part_length: 2 * part_length]
    part3 = frames[2 * part_length:]

    # Reverse the first two parts
    reversed_part1 = part1[::-1]
    reversed_part2 = part2[::-1]

    # Adhere the reversed parts
    result = reversed_part1 + reversed_part2

    # Open the output sound file
    with wave.open(output_file, 'wb') as wav_out:
        # Set the parameters for the output sound
        wav_out.setparams(params)

        # Write the result to the output sound file
        wav_out.writeframes(result)

# Example usage
input_sound = r"D:\Xu_Haoxin\Research\Gradu_thesis\Code\Vioce_shuffle\BigPhee23full.wav"
output_sound = r"D:\Xu_Haoxin\Research\1_3_reverse_switch.wav"
cut_reverse_adhere_sound(input_sound, output_sound)