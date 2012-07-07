file = File.new("patterns.txt","r");
lines = []
i=0;
while (line = file.gets)
   lines[i] = line;
   i = i+1;
end
while true
lines.each do |x|
 puts x
 system("/usr/bin/python "+x);
end
end

