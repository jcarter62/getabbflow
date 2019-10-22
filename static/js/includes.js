function startup() {
    let collection = document.getElementsByClassName('sitestatus');
    for (var c in collection) {
        // console.log( collection[c] )
        let id = collection[c].id;
        if (id != null) {
            document.getElementById(id).innerText = ' *zzz* ';
            thisurl = '/getdata/' + id;
            // if ( id == '14l') {
            fetch(thisurl).then(function (response) {
                response.json().then(function (data) {
                    //
                    let total_flow = 0.0;
                    for (let i in data.flow) {
                        let flo = data.flow[i];
                        // console.log(flo)
                        if (flo.tag == 'TOTAL') {
                            total_flow = flo.value;
                        }
                    }
                    document.getElementById(id).innerText = total_flow.toString();
                });
            });
            // }
        }
    }
}
