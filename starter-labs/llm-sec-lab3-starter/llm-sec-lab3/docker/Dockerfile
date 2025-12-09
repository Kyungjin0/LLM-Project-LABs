
FROM nginx:1.23.4
USER root
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://example.com/install.sh | sh
CMD ["bash"]
