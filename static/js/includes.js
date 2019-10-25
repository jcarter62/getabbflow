
function startup() {
    let collection = document.getElementsByClassName('sitestatus');
    for (var c in collection) {
        // console.log( collection[c] )
        let id = collection[c].id;
        if (id != null) {
//            document.getElementById(id).innerText = ' Loading ...';
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

function reload_site(site) {
    let id = find_id_by_sitename(site);
    if (id != null) {
        document.getElementById(id).classList.add('siteloading');
        let thisurl = '/getdata/' + id;
        fetch(thisurl).then(function (response) {
            response.json().then(function (data) {
                //
                let result = '';
                if (data.acft.length <= 0) {
                    result = 'Timeout';
                } else {
                    let total_flow = 0.0;
                    for (let i in data.flow) {
                        let flo = data.flow[i];
                        // console.log(flo)
                        if (flo.tag == 'TOTAL') {
                            total_flow = flo.value;
                        }
                    }
                    result = total_flow.toString();
                }
                document.getElementById(id).innerText = result;
                document.getElementById(id).classList.remove('siteloading');

            });
        });
    }
}

function find_id_by_sitename(sitename) {
    let id = null;
    let collection = document.getElementsByClassName('sitestatus');
    for (var c in collection) {
        id = collection[c].id;
        if (id != null) {
            // if matched, then exit loop.
            if (id == sitename) {
                break;
            }
        }
    }
    return id;
}

let countdown_from = 120;
let countdown_timer = 0;

function timerHandler() {
    setInterval(function () {
        countdown_timer--;
        document.getElementById('countdown').innerText = countdown_timer.toString();
        if (countdown_timer < 0) {
            countdown_timer = countdown_from;
            startup();
        }
    }, 1000);
}
