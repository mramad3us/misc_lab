#!/usr/bin/ruby

#inf = File.binread("ed70.pdf",512,0)

begin
    cleav_sz = 34096

    inf = File.open("ed70.pdf")
    header = inf.read(cleav_sz)
    inf.seek(cleav_sz,:CUR)
    footer = inf.read(inf.size)

    ctrlbuf = "DEADBEEF"*6400024

    binbuf = [ctrlbuf].pack("H*")
    data = header + binbuf + footer

    outf = File.open("test.pdf","w+")
    outf.write(data)
ensure
    inf.close if inf 
    outf.close if outf
end

