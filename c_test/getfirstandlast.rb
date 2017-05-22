#!/usr/bin/ruby

File.open("toto.txt","r+") do |f|
    puts("First line : %s" % f.gets(15))
    f.seek(3000)
    puts("last line : %s" % f.gets)
end
