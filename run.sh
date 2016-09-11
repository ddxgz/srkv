go install github.com/ddxgz/srkv


if [ $? -eq 0 ]; then
    echo Build OK
    $GOPATH/bin/srkv
else
    echo Build FAIL
fi
#
