package com.mendhak.gpslogger.senders.customurl;

import android.app.Application;
import android.net.wifi.WifiManager;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import androidx.appcompat.app.AppCompatActivity;
import android.net.wifi.WifiInfo;



public class GetWifi extends Application {
    public int getwifi(){
        WifiManager wifiManager;
        Context mc = getApplicationContext();
        wifiManager = (WifiManager) mc.getSystemService(Context.WIFI_SERVICE);
//        if(wifiManager.getWifiState() == WifiManager.WIFI_STATE_ENABLED){
//            System.out.println("WIFI ENABLED");
//        }
//        else{
//            System.out.println("WIFI NOT ENABLED");
//        }
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int rssi = wifiInfo.getRssi();
        return rssi;
    }
};
