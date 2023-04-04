#!/bin/bash



sudo apt install -y apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install -y bazel

git clone -b v22.2 git@github.com:protocolbuffers/protobuf.git
pushd protobuf
git submodule update --init --recursive
bazel build :protoc :protobuf
sudo cp bazel-bin/protoc /usr/local/bin
popd

sudo apt -y install libprotobuf-dev libprotoc-dev protobuf-compiler

git clone -b v1.4.1 git@github.com:protobuf-c/protobuf-c.git
pushd protobuf-c
./autogen.sh
./configure
make
sudo make install
popd

echo "Finished installation"



 

