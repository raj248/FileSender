import sys, filetransitSender

f = open('content.txt','a+')
for i in sys.argv:
	if i==' ' or i==sys.argv[0]:
		continue

	f.write(i)
f.close()

filetransitSender.Send()