package com.intelligester;

import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import java.io.*;

import com.emotiv.*;

public class EmotivWrapper {
    static Pointer eEvent			= Edk.INSTANCE.EE_EmoEngineEventCreate();
    static Pointer eState	        = Edk.INSTANCE.EE_EmoStateCreate();
    static IntByReference userID 	= null;
    static short composerPort	   	= 1726;
    static int debugMode       		= System.getProperty("DEBUG") != null ? 1 : 0;
    static int state    	    	= 0;
    static int startindex           = 30; // adjust these values if you wish
    static int endindex             = 60;
    static double thresholdamt      = 0.20;

    public static void connect() {
        userID = new IntByReference(0);

    	switch (debugMode) {
		case 0:
		{
			if (Edk.INSTANCE.EE_EngineConnect("Emotiv Systems-5") != EdkErrorCode.EDK_OK.ToInt()) {
				System.out.println("Emotiv Engine start up failed.");
				return;
			}
			break;
		}
		case 1:
		{
			System.out.println("Target IP of EmoComposer: [127.0.0.1] ");

			if (Edk.INSTANCE.EE_EngineRemoteConnect("127.0.0.1", composerPort, "Emotiv Systems-5") != EdkErrorCode.EDK_OK.ToInt()) {
				System.out.println("Cannot connect to EmoComposer on [127.0.0.1]");
				return;
			}
			System.out.println("Connected to EmoComposer on [127.0.0.1]");
			break;
		}
		default:
			System.out.println("Invalid option...");
			return;
    	}
    }

    public static void disconnect() {
    	Edk.INSTANCE.EE_EngineDisconnect();
    	System.out.println("Disconnected!");
    }

    public static void pollForever() {
        int counter = 0; // used for undersampling
        int initcount = 0;
        double sum = 0.0;
        double baseval = 0.0;
        double ub = 0.0;
        double lb = 0.0;
        int onecount = 0;
        double previous = 0.0;
		while (true)
		{
			state = Edk.INSTANCE.EE_EngineGetNextEvent(eEvent);

			// New event needs to be handled
			if (state == EdkErrorCode.EDK_OK.ToInt()) {

				int eventType = Edk.INSTANCE.EE_EmoEngineEventGetType(eEvent);
				Edk.INSTANCE.EE_EmoEngineEventGetUserId(eEvent, userID);

				// Log the EmoState if it has been updated
				if (eventType == Edk.EE_Event_t.EE_EmoStateUpdated.ToInt()) {
                    
                    Edk.INSTANCE.EE_EmoEngineEventGetEmoState(eEvent, eState);
                    
                    if(initcount < endindex) {
                        if(initcount > startindex) {
                            // System.out.println(sum);
                            sum += EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState);
                        }
                    }
                    
                    else if(initcount == endindex) {
                        baseval = sum / (double)(endindex-startindex);
                        ub = baseval + thresholdamt;
                        lb = baseval - thresholdamt;
                    }
                    
                    else {
                        // Edk.INSTANCE.EE_EmoEngineEventGetEmoState(eEvent, eState);
                        /*float timestamp = EmoState.INSTANCE.ES_GetTimeFromStart(eState);
                        try {
                            BufferedWriter log = new BufferedWriter(new OutputStreamWriter(System.out));
                            log.write(timestamp + " : New EmoState " + EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState) + " from user " + userID.getValue() + " counter " + counter + " action " + EmoState.INSTANCE.ES_CognitivGetCurrentAction(eState) + " baseval " + baseval);
                            log.flush();
                        }
                        catch (Exception e) {
                            e.printStackTrace();
                        }*/
                        try {
                            //System.out.println("Value: " + counter);
                            BufferedWriter log = new BufferedWriter(new OutputStreamWriter(System.out));
                            if(counter == 3) {
                                    double deviation = Math.abs(EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState)-baseval);
                                    if(deviation > thresholdamt) {
                                        log.write(Integer.toString(1));
                                        log.flush();
                                        onecount++;
                                        if(onecount >= 10) {
                                            baseval = EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState);
                                            onecount = 0;
                                        }
                                    }
                                    else {
                                        log.write(Integer.toString(0));
                                        log.flush();
                                        if(previous > EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState)) {
                                            baseval = EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState);
                                        }
                                    }
                                    counter = 0;
                            }
                            previous = EmoState.INSTANCE.ES_AffectivGetExcitementShortTermScore(eState);
                        }
                        catch (Exception e) {
                                e.printStackTrace();
                        }
                        counter++;

                        //System.out.print("WirelessSignalStatus: ");
                        //System.out.println(EmoState.INSTANCE.ES_GetWirelessSignalStatus(eState));

                        // float boredomScore = EmoState.INSTANCE.ES_AffectivGetEngagementBoredomScore(eState);
                        // float medScore = EmoState.INSTANCE.ES_AffectivGetMeditationScore(eState);
                    }

                    initcount++;
                }
			}
			else if (state != EdkErrorCode.EDK_NO_EVENT.ToInt()) {
				System.out.println("Internal error in Emotiv Engine!");
				break;
			}
        }
        disconnect();
    }

}
