<?php
/**
 * Created by PhpStorm.
 * User: KeOndrae
 * Date: 2019-10-04
 * Time: 15:08
 */

require_once '../php/IoTDevices.php';

$Calling = $_GET['Calling'];



switch ($Calling){

    case 'GetIoTDevicesInRoom':
        GetIoTDevicesInRoom();
        break;
}

function GetIoTDevicesInRoom()
{

   if (isset($_GET['RoomID'])) {

        $RoomID = $_GET['RoomID'];

        $IoTDevices = new IoTDevices();
        $results = $IoTDevices->GetIoTDevicesInRoom($RoomID);
        echo json_encode($results);


    }else{

       echo json_encode('Post Error - GetIoTDevicesInRoom');
   }
}