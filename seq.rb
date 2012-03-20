file = File.new("patterns.txt","r");
lines = []
i=0;
while (line = file.gets)
   lines[i] = line;
   i = i+1;
end

lines.each do |x|
 puts x
 system("python "+x);
end

