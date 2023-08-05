# Use the official image as a parent image
FROM debian

# Update the system
RUN apt-get update

# Install OpenSSH Server and python interpreter
RUN apt-get install -y openssh-server 
RUN apt-get upgrade -y
RUN apt-get install -y python3
 
# Set up configuration for SSH
RUN mkdir /var/run/sshd
RUN echo 'root:cisco' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
 
# SSH login fix. Otherwise, user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
 
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
 
# Expose the SSH port
EXPOSE 22
EXPOSE 80
EXPOSE 443
 
# Run SSH
CMD ["/usr/sbin/sshd", "-D"]