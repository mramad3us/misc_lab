#!/usr/bin/ruby


File.open("clean_2p.ets","rb") do |f|
	mut=0
	while raw=f.read(1).unpack("C")
        raw=raw[0]
	    puts(raw)
	end
	mut=~raw.to_i
	puts(mut.to_s(2))
end
