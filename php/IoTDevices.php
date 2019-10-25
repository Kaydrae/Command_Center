<?php
/**
 * Created by PhpStorm.
 * User: KeOndrae
 * Date: 2019-09-17
 * Time: 19:26
 */

require_once "../Connection/Connection.php";

class IoTDevices
{

    public function __construct()
    {

    }

    public function __destruct()
    {
        // TODO: Implement __destruct() method.
    }

    public function GetIoTDevice($deviceID)
    {
        // TODO: Implement __get() method.
    }

    public function GetIoTDevicesInRoom($roomID)
    {
        //echo $roomID;
        $conn = new Connection();
        if($conn->Connect()){
            $dataArray[] = array();
            $query = "SELECT * FROM IoTDevice WHERE Room_ID = ? AND Enable = ?";
              $result = $conn->Connect()->prepare($query);
               $result-> execute([$roomID, 1]);
                $data = $result-> fetchall();

               foreach ($data as $row) {

                  $typeQuery = "SELECT Name FROM Type WHERE ID = ? AND Enable = ?";
                   $typeResult = $conn->Connect()->prepare($typeQuery);
                   $typeResult-> execute([$row['Type'],1]);
                   $type = $typeResult-> fetch();

                   $dataArray[] = array(
                       'ID'         => $row['ID'],
                       'Name'       => $row['Name'],
                       'IP'         => $row['IP'],
                       'RoomID'     => $row['Room_ID'],
                       'Hostname'   => $row['Hostname'],
                       'ImageNumber'=> $row['ImageNumber'],
                       'Type'       => $type

                   );
               }

            $conn->Disconnect();
            return $dataArray;


        }else {
            echo json_encode('error');

        }
    }

    public function DisplayIoTDevices(){

    }

    public function DisplayFavIoTDevices(){

    }
}