import os, socket, sys, urllib, urllib2, time

class sub-checker():

    def TestUpload(self):
    # Testing upload speed

        url="upload.php?x=" + str( time.time() )

        sizes, took=[0,0]
        counter=0
        failures=0
        data=""
        for i in range(0, len(self.upSizes)):
            if len(data) == 0 or self.upSizes[i] != self.upSizes[i-1]:
                #print_debug("Generating new string to upload. Length: %d\n" % (self.upSizes[i]))
                data=''.join("1" for x in xrange(self.upSizes[i]))
            self.postData=urllib.urlencode({'upload6': data })
            
            sizes, took=self.AsyncRequest(url, 1)
            #sizes, took=self.AsyncRequest(url, (i<4 and 1 or (i<6 and 2 or (i<6 and 4 or 8))), 1)
            
            # Stop testing if too many failures            
            counter=counter+1
            if sizes==0:
                failures=failures+1
                if failures>2:
                    break
                continue

            size=self.SpeedConversion(sizes)
            speed=size/took
            print_debug("Upload size: %0.2f MiB; Uploaded in %0.2f s\n" % 
                (size, took))
            print_debug("\033[92mUpload speed: %0.2f %s/s\033[0m\n" % 
                (speed, self.units))
            
            if self.up_speed<speed:
                self.up_speed=speed

            if took>5 or counter>=self.uploadtests:
                break
                
        #print_debug("Upload size: %0.2f MiB; Uploaded in %0.2f s\n" % (self.SpeedConversion(sizes), took))
        #print_debug("Upload speed: %0.2f MiB/s\n" % (self.SpeedConversion(sizes)/took))

    def SpeedConversion(self, data):
        if self.unit==1:
            result=(float(data)/1024/1024)
        else:
            result=(float(data)/1024/1024)*1.048576*8
        return result

    def TestDownload(self):
    # Testing download speed
        sizes, took=[0,0]
        counter=0
        failures=0
        for i in range(0, len(self.downList)):
            url="random"+self.downList[i]+".jpg?x=" + str( time.time() ) + "&y=3"
            
            sizes, took=self.AsyncRequest(url)
            #sizes, took=self.AsyncRequest(url, (i<1 and 2 or (i<6 and 4 or (i<10 and 6 or 8))) )
            
            # Stop testing if too many failures            
            counter=counter+1
            if sizes==0:
                failures=failures+1
                if failures>2:
                    break
                continue

            size=self.SpeedConversion(sizes)
            speed=size/took
            print_debug("Download size: %0.2f MiB; Downloaded in %0.2f s\n" % 
                (size, took))
            print_debug("\033[91mDownload speed: %0.2f %s/s\033[0m\n" % 
                (speed, self.units))

            if self.down_speed<speed:
                self.down_speed=speed

            if took>5 or counter>=self.downloadtests:
                break

        #print_debug("Download size: %0.2f MiB; Downloaded in %0.2f s\n" % (self.SpeedConversion(sizes), took))
        #print_debug("Download speed: %0.2f %s/s\n" % (self.SpeedConversion(sizes)/took, self.units))
