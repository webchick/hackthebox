FROM ubuntu:20.04

# Setup environment variables
ENV user ctf
ENV prob_port 13131
ENV flag flag
ENV bin controller

# Install packages
RUN apt-get update 
RUN apt-get install -y socat python3

# Change permission
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Copy binaries and flag
RUN adduser $user
ADD ./server.py /home/$user/server.py
ADD ./$bin /home/$user/$bin
ADD ./$flag /home/$user/$flag
RUN chown -R root:root /home/$user/
RUN chown root:$user /home/$user/server.py
RUN chown root:$user /home/$user/$bin
RUN chown root:$user /home/$user/$flag
RUN chmod 2755 /home/$user/server.py
RUN chmod 2755 /home/$user/$bin
RUN chmod 440 /home/$user/$flag

# final
CMD socat TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/server.py
USER $user
EXPOSE $prob_port
