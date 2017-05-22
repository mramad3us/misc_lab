#!/usr/bin/ruby

File.open("toto.txt","w+") do |f|
    startf = File.read("starter")
    pld = "#{startf}deadbeef"
    f.write(pld)
end

