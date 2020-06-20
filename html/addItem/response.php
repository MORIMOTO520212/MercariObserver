<?php

function getTransaction() {
    return file_get_contents("../../data/transaction.json");
}
function getMercari_selling() {
    return file_get_contents("../../data/mercari_selling.json");
}

if ( isset($_GET['mode']) ) {
    switch ($_GET['mode']) {
        case 'transaction':
            $data = getTransaction();
            break;
        case 'mercari_selling':
            $data = getMercari_selling();
            break;
    }
    echo $data;
}
?>