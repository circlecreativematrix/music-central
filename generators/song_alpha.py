class Song():
	def __init__(self):
		self.output = []
	def main(self):
		tempo = 120
		keynote = "D4"
		keytype = "major"
		self.add_header(tempo, keynote, keytype)
		self.gen_scale(0, 8, step=1)
		self.gen_scale(7, -1, step=1)
		print(self.out())
	def append(self, string):
		self.output.append(string)
	def out(self):
		return "\n".join(self.output)
	def add_header(self, tempo, keynote, keytype):
		self.append(f"tempo:{tempo},key_note:{keynote},key_type:{keytype}")

	def gen_scale(self, start, end, step=1, timing=["1/8","1/8","1/8","1/8"]):
		minus = 1
		note = "P+1"
		if start > end:
			minus = -1
			note = "P-1"
		for i in range(start, end, step*minus):
			timedur = timing[i%len(timing)]
			self.append(f"note:{note},time:P+{timedur},dur:{timedur}")
			
if __name__ == "__main__":
	song = Song()
	song.main()