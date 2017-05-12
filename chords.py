import sys
import os
from operator import itemgetter
import math
import pygame, pygame.sndarray
import time, random
import numpy
import scipy.signal
import sys, os
import termios, fcntl 

#user notes is an array that will hold the corresponding notes to be played depending on the coordinates
userNotes = []

sample_rate = 44100
sampling = 4096 

#array of notes and corresponding frequency in HZ which they can be played at
Notes = { "Ab" : 415.3, "A" : 440.0, "A#" : 466.16,
		  "Bb" : 466.16, "B" : 493.88,
						 "C" : 523.25, "C#" : 554.37,
		  "Db" : 554.37, "D" : 587.33, "D#" : 622.25,
		  "Eb" : 622.25, "E" : 659.25,
						 "F" : 698.46, "F#" : 739.99,
		  "Gb" : 739.99, "G" : 783.99, "G#" : 830.61
		}

def sine_wave(hz, peak, n_samples=sample_rate):
	"""Compute N samples of a sine wave with given frequency and peak amplitude.
	   Defaults to one second.
	"""
	length = sample_rate / float(hz)
	omega = numpy.pi * 2 / length
	xvalues = numpy.arange(int(length)) * omega
	onecycle = peak * numpy.sin(xvalues)
	return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)

def parse_chord(ns, default_duration=300):
    '''Parse a single chord notation, like E4,G4:2.
       Returns a list of frequencies (possibly empty) and a duration in ms.
    '''
    if ':' in ns:
        ns, durationstr = ns.strip().split(':')
        # everything after the colon is a duration
        duration = float(durationstr.strip())
    else:
        duration = 1.
    duration = int(duration * default_duration)

    freqlist = []
    indnotes = ns.strip().split(',')
    chord = None
    for ns in indnotes:
        if ns[0] in Notes:
            if len(ns) > 1 and (ns[1] == 'b' or ns[1] == '#'):
                # It's a sharp or flat
                freqlist.append(Notes[ns[:2]])
                ns = ns[2:]
            else:
                # No sharp or flat
                freqlist.append(Notes[ns[0]])
                ns = ns[1:]
            try:
                octave = float(ns)    # which octave is it?
                freqlist[-1] *= 2 ** (octave-1)
                ns = ns[1:]
            except:
                pass
    return freqlist, duration
#open the save file and read in the notes array
def play_notes(notestring, waveform=None):
    '''notestring is a string with a format like this:
    D4,F4 E4,G4:2 Bb3   note#octave,note#octave:duration
    where either octave or duration can be omitted to use the default (1).
    Duration can be a decimal.
    # or b can follow a note letter.
    Omit the note to indicate a rest, e.g. :1.
    '''
    if not waveform:
        waveform = sine_wave

    for ns in notestring.split():
        freqlist, duration = parse_chord(ns)
        if freqlist:
            chord = waveform(freqlist[0], sampling)
            for freq in freqlist[1:]:
                chord = sum([chord, waveform(freq, sampling)])
            play_for(chord, duration)
        else:
            # If we didn't get any frequencies, then rest.
            pygame.time.delay(duration)
        pygame.time.delay(80)

def play_for(sample_wave, ms):
    """Play given samples, as a sound, for ms milliseconds."""
    # In pygame 1.9.1, we can pass sample_wave directly,
    # but in 1.9.2 they changed the mixer to only accept ints.
    sound = pygame.sndarray.make_sound(sample_wave.astype(int))
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

def getNotes():
	with open('test.txt') as f:
		content = f.readlines()
		content = [x.strip() for x in content]
	#print content #check it's read in correctly

	#print '\n'

	#convert list of string to list of ints
	#num_contents = [int(i) for i in content]
	num_contents = map(int, content)
	#print num_contents

	#print '\n'

	#convert the array into a list of tuples which will map to be coordinate pairs
	if(len(num_contents)%2==0):
		#print 'Number of contents is even'
		pairs = zip(num_contents[::2], num_contents[1::2])
		#print pairs
	else:
		#print 'Number of contents is odd' #add 0 to make it even
		num_contents.append(0)
		pairs = zip(num_contents[::2], num_contents[1::2])
		#print pairs

	#get high and low for pairs to get the range(y values)
	#get max y value
	max_y = max(pairs,key=itemgetter(1))[1]
	#print max_y
	#get min y value
	min_y = min(pairs,key=itemgetter(1))[1]
	#print min_y

	#get range of y values then divide it by 17(17 notes in our array)
	y_range = max_y - min_y
	#print y_range
	step = math.ceil(y_range / 17.0) #if its even a bit over a whole number we want the next greatest integer to make sure we hit the max value or above the max value so it doesn't get included
	#print step
	y_steps = []
	y_steps = range(min_y, (max_y+int(step)), int(step))
	#print y_steps

	#get all y values to make the resulting user_notes array
	y_vals = [x[1] for x in pairs]
	#print y_vals

	#convert y values to note formats, use if/elif
	for idx, val in enumerate(y_vals):
		#print idx, val
		if(y_steps[0] <= val < y_steps[1]):
			#print 'Val between first and second index of y_steps'
			userNotes.append("Ab")
		elif(y_steps[1] <= val < y_steps[2]):
			userNotes.append("A")
		elif(y_steps[2] <= val < y_steps[3]):
			userNotes.append("A#")
		elif(y_steps[3] <= val < y_steps[4]):
			userNotes.append("Bb")
		elif(y_steps[4] <= val < y_steps[5]):
			userNotes.append("B")
		elif(y_steps[5] <= val < y_steps[6]):
			userNotes.append("C")
		elif(y_steps[6] <= val < y_steps[7]):
			userNotes.append("C#")
		elif(y_steps[7] <= val < y_steps[8]):
			userNotes.append("Db")
		elif(y_steps[8] <= val < y_steps[9]):
			userNotes.append("D")
		elif(y_steps[9] <= val < y_steps[10]):
			userNotes.append("D#")
		elif(y_steps[10] <= val < y_steps[11]):
			userNotes.append("Eb")
		elif(y_steps[11] <= val < y_steps[12]):
			userNotes.append("E")
		elif(y_steps[12] <= val < y_steps[13]):
			userNotes.append("F")
		elif(y_steps[13] <= val < y_steps[14]):
			userNotes.append("F#")
		elif(y_steps[14] <= val < y_steps[15]):
			userNotes.append("Gb")
		elif(y_steps[15] <= val < y_steps[16]):
			userNotes.append("G")
		elif(y_steps[16] <= val <= y_steps[17]):
			userNotes.append("G#")

	#print userNotes
	noteString = ' '.join(userNotes)
	#print noteString
	#return userNotes
	return noteString

def playSound():
	pygame.mixer.pre_init(sample_rate, -16, 1) # 44.1kHz, 16-bit signed, mono
	pygame.init()
	notes = getNotes()
	#print notes 
	play_notes(notes)

# def main():
# 	pygame.mixer.pre_init(sample_rate, -16, 1) # 44.1kHz, 16-bit signed, mono
# 	pygame.init()
# 	notes = getNotes()
# 	#print notes 
# 	play_notes(notes)

# if __name__ == '__main__':
# 	main()
