#!/usr/bin/ruby
#Last modified : 28/05/2017
#By : Mramad3us

module Spiker
    def Spiker.insert(inf,outf,hexstr,head_sz=512)
        puts("Insert function is obsolete, use Spiker.charfill")
    end

    def Spiker.bitflip(idata,verbose)
        #Flip all bits from input and return result
        #If verbose is true, output detail (To improve with negative numbers...)
        to_ret = ""
        idata.chars.each do |c|
            raw = c.unpack("C")[0]
            puts("[ Bitflip ] In : #{raw.to_s(2)}") if verbose
            flipped = ~raw 
            puts("[ Bitflip ] Out : #{flipped.to_s(2)}") if verbose
            to_ret += [flipped].pack("C")
        end
        return to_ret
    end

    def Spiker.charfill(idata,verbose,char='A')
        #Change every character in input data 'idata' to char
        if char.size==1
            return char*idata.size
        else
            puts("[ Charfill error ]  Char should be size 1")
            return 0
        end
    end
end
    
class SpikedFile
    def initialize(outf_name,padding='41',outf_type="wb",name="***")
        @name = name 
        @to_insert = []
        @content = "" 
        @outf = File.new(outf_name,outf_type)
        @padding = [padding].pack("H*") #Defaults to 0x41
        @f_cursor = 0 #Current position in outf
        @v_cursor = 0 #Virtual cursor for defualt array building
        @outf_name = outf_name
    end

    def cleanup
        @outf.close if not @outf.nil?
    end

    def size
        if mk_content
            return @content.size
        else
            log("Error calculating size","ERROR")
            return 0 
        end
    end

    def log(msg="no message",tag=@name)
        puts("[ #{tag} ]  #{msg}")
    end

    def insert(data,enc="H*",offset=@v_cursor)
        #Insert data at @outf offset, padding the way in between
        #Don't pass an offset value to append.
        #Warning : Can't mix both modes for a single session.
        if data.nil?
            log("No data to insert, aborting","ERROR")
            return false
        end

        #log("Insert #{data} @ #{offset}","Debug")

        @to_insert.each do |e_data,e_enc,e_offset| #Check if offset is already reserved
            if e_offset == offset
                log("Redundant offset:#{offset}, aborting...","ERROR")
                cleanup
                return false
            elsif e_offset < 0
                log("Negative offset, aborting...","ERROR")
                cleanup
                return false
            end
        end

        @to_insert.push([data,enc,offset])
        @v_cursor += ([data].pack(enc)).size

        return true
    end

    def mk_content
        #Build the content string from to_insert array
        @f_cursor = 0
        @content = ""
        @to_insert = @to_insert.sort_by{|data,encoding,offset| offset}

        @to_insert.each do |data,encoding,offset|
            #log("offset : #{offset} , f_cursor : #{@f_cursor}","Debug")
            
            if offset < @f_cursor
                log("Bad offsets/sizes : off=#{offset} cur=#{@f_cursor} #{@to_insert}",
                    "ERROR")
                cleanup
                return false
            end

            @content << @padding*(offset-@f_cursor)
            @content << [data].pack(encoding)

            @f_cursor = @content.size #Put file cursor to the end of data

            #log("Pushing #{data} @ #{offset}...New cursor @ #{@f_cursor}","Debug")
        end
        return true
    end

    def dump
        #Dump data to file
        return false if not mk_content
        log "Dumping to file..."

        out_size = @outf.write(@content)
        log "Written #{out_size}B to #{@outf_name}"
        cleanup
        return true
    end

    def self.open(outf_name,padding='41',outf_type="wb",name="***")
        yield spiked = new(outf_name,padding,outf_type,name)
        if not spiked.dump
            spiked.log("Couldn't dump to file...","ERROR")
            spiked.cleanup
        end
    end
end

class FuzzedFile < SpikedFile
    include Spiker
    def initialize(inf_name,outf_name='fuzzedfile.fz',verbose=false)
        super(outf_name=outf_name)
        @inf = File.new(inf_name,"rb")
        @inf_name = inf_name
    	@verbose = verbose
    end 

    def cleanup
        @inf.close if not @inf.nil?
        super
        return true
    end

    def mk_content
        begin
            @content = @inf.read if @content.size == 0
        rescue
            log("Error reading input file","ERROR")
            return false
        end

        #log("Content is #{@content}","DBG")

        return true
    end

    def mutate(offst_start,offst_end=nil,method='bitflip',char='A')
        #Mutate string between offst_start and offst_end in @content 
        #return false if failed, otherwise return true
        #If offst_end not specified, mutate from start to eof

        #log("Size is #{size}","DBG")
        mk_content
        if offst_end.nil?
            offst_sz = size
            offst_end = size - 1 #Put cursor to eof
        elsif offst_end > size
            log("Wrong size, check offsets","ERROR")
            return false
        else
            if offst_end < offst_start
                log("End offset bigger than start...","ERROR")
                return false
            end

            offst_sz = offst_end - offst_start
        end

        to_mut = @content[offst_start,offst_sz]
        if to_mut.nil?
            log("Nothing to mutate","ERROR")
            return false
        end
        
        case method
        when 'bitflip'
            mutated = Spiker.bitflip(to_mut,@verbose)
        when 'charfill'
            mutated = Spiker.charfill(to_mut,@verbose,char)
        else
            log("#{method} isn't a valid mutation method","Mutate error")
        end

        #log("mutated is #{mutated} size is #{mutated.size}","DBG")
        
        #Reassemble string
        starter = @content[0,offst_start]
        footer = @content[offst_end,size]
        
        @content = starter+mutated+footer
        return true
    end

    def self.open(inf_name,outf_name,verbose)
        yield fuzfile = new(inf_name,outf_name,verbose)
        if not fuzfile.dump
            fuzfile.log("Error when dumping to file","ERROR")
            fuzfile.cleanup
        end
    end
end

        
