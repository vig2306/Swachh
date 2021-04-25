import React, { useState, useEffect } from 'react';
import { Camera } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import { Col, Row, Grid } from "react-native-easy-grid";
import { View, TouchableWithoutFeedback, TouchableOpacity, Modal, Text, TextInput } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { MaterialIcons } from '@expo/vector-icons';
import styles from '../constants/styles';
import * as Location from 'expo-location';
import axios from "axios";    
import Constants from '../constants/text';
import AsyncStorage from "@react-native-community/async-storage";
import ModalButton from '../components/modalButton';
import Colors from '../constants/colors';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { Entypo } from '@expo/vector-icons';
import RadioForm, {
    RadioButton,
    RadioButtonInput,
    RadioButtonLabel,
  } from "react-native-simple-radio-button";

export default function Toolbar({ cameraRef, navigation }) {
    const [location, setLocation] = useState(null);
    const [errorMsg, setErrorMsg] = useState(null);
    const [userData, setuserData] = useState({});
    const [modalVisible, setModalVisible] = useState(false);
    const [priority, onChangePriority] = useState("");

    const custom_values = {
        name: "abc",
        email: "abc",
        phone: "abc",
      };
    var radio_props = [
    { label: "Low ", value: 0 },
    { label: "Medium ", value: 1 },
    { label: "High ", value: 2 },
    ];
    const [name, onChangeName] = useState(null);
    useEffect(() => {
        (async () => {
            let { status } = await Location.requestPermissionsAsync();
            if (status !== 'granted') {
                setErrorMsg('Permission to access location was denied');
            }

            let location = await Location.getCurrentPositionAsync({});
            setLocation(location);
        })();
    });

    const resetModalInfo = () => {
        onChangeName('')
        onChangePriority("");
    }
    const editProfile = () => {
        Keyboard.dismiss()
        var data = {}
        if (name) {
            data['name'] = name
        }
        if (email) {
            data['email'] = email
        }
        data['id'] = 'X8E6gpS3CjHhA3FuhcnM'
        data['societyId'] = 'NXZyFd6qMbzJPtBPygoq'
        console.log(data)
        try {
            axios.post("https://us-central1-sahayak-a912a.cloudfunctions.net/app/edit_profile", data).then(response => {
                console.log(response.data);
                if (response.status == 200) {
                    ToastAndroid.showWithGravityAndOffset(
                        response.data.message,
                        ToastAndroid.LONG,
                        ToastAndroid.BOTTOM,
                        25,
                        50
                    );
                }
                setModalVisible(false)
            })
        } catch (error) {
            if (response.status == 200) {
                ToastAndroid.showWithGravityAndOffset(
                    "error while adding into notices : "+error,
                    ToastAndroid.LONG,
                    ToastAndroid.BOTTOM,
                    25,
                    50
                );
            }
            setModalVisible(false)
        }
    };


    const [capturing, setCapturing] = useState(false)
    const [image, setImage] = useState(null)
    const [IsImage, setIsImage] = useState(false)

    async function takePicture() {

        if (cameraRef) {
            setCapturing(true)
            const options = { quality: 0.1, base64: true, uri: true };
            let photo = await cameraRef.takePictureAsync(options);
            setCapturing(false)
            setIsImage(true)
            setImage(photo.base64)
            await cameraRef.pausePreview()
        }

    }

    async function uploadData() {
        setIsImage(false)
        let response=await AsyncStorage.getItem("userData")
        
        response = JSON.parse(response);
        console.log('\n\n\n\noriginal data:'+JSON.stringify(response.data.user_email))
        let location = await Location.getCurrentPositionAsync({});
       
        const data = {
            "image_link": image,
            "grievance_id": Math.random().toString(36).substring(7),
            "user_id": response.data.user_email,
            "grievance_type": "unpredicted",
            "latitude": location.coords.latitude,
            "longitude": location.coords.longitude,
            "priority": priority,
        }

        console.log('this is your data: ' + JSON.stringify(data))
        axios
            .post(`${Constants.ApiLink}/uploader`, data)
            .then(async function (response) {
                // handle success

                try {
                    const jsonValue = JSON.stringify(response.data);
                    await AsyncStorage.setItem("value", jsonValue);
                    console.log("data: " + jsonValue);
                } catch (e) {
                    // saving error
                    console.log("Got error while storing data to async" + e);
                }
            })
            .catch(function (error) {
                // handle error
                console.log("ERROR ON HOME", error);
            })
            .finally(function () {
                // always executed
            });
        // console.log('This is my base 64 image', image)
        await cameraRef.resumePreview()
    }

    async function account() {
        navigation.navigate('Profile')
    }

    return (
        <Grid style={styles.bottomToolbar}>
            <Row>
                <Col style={styles.alignCenter}>
                    <TouchableOpacity onPress={() => navigation.navigate('EntryRecords')}>
                        <MaterialIcons name="history" size={30} color="white" />
                    </TouchableOpacity>
                </Col>

                <Col size={2} style={styles.alignCenter}>
                    <TouchableWithoutFeedback
                        onPress={takePicture}>
                        <View style={[styles.captureBtn, capturing && styles.captureBtnActive]}>
                            {capturing && <View style={styles.captureBtnInternal} />}
                        </View>
                    </TouchableWithoutFeedback>


                </Col>
                {
                    IsImage ?
                        <Col style={styles.alignCenter}>
                            <TouchableOpacity onPress={() => { setModalVisible(true); }}>
                                <Feather name="check" size={30} color="white" />
                            </TouchableOpacity>
                        </Col> : <Col style={styles.alignCenter}>
                            <TouchableOpacity onPress={account}>
                                <MaterialCommunityIcons name="account" size={30} color="white" />
                            </TouchableOpacity>
                        </Col>
                    
                }
            </Row>
            <Modal
                        animationType="fade"
                        transparent={true}
                        visible={modalVisible}
                        onRequestClose={() => { setModalVisible(!modalVisible); resetModalInfo() }}
                    >
                        <View style={styles.centeredView}>
                            <View style={styles.modalView}>
                                <View style={{ flexDirection: "row", alignItems: "center",marginBottom: hp("4%") }}>
                                    <View style={{ alignItems: "flex-start", justifyContent: "flex-start" }}>
                                        <Text style={styles.modalHeader}>Add Priority</Text>
                                    </View>
                                    <View style={{ backgroundColor: Colors.primaryColor, padding: wp("0.5%"), borderRadius: 5, justifyContent: "flex-end", marginLeft: "auto" }}>
                                        <Entypo name="cross" size={16} color="white" onPress={() => { setModalVisible(!modalVisible); resetModalInfo() }} />
                                    </View>
                                </View>
                                 <RadioForm
                                    radio_props={radio_props}
                                    initial={0}
                                    formHorizontal={true}
                                    labelHorizontal={true}
                                    buttonColor={Colors.primaryColor}
                                    buttonSize={10}
                                    animation={true}
                                    labelStyle={{ marginRight: wp("6%"),marginBottom: hp("2%")  }}
                                    onPress={(value) => {
                                    onChangePriority(value);

                                }}
                               />              
                                <View>
                                <TouchableOpacity style={{ justifyContent: "center", alignItems: "center", backgroundColor: Colors.primaryColor,padding:hp("1.8%"),borderRadius:15,marginTop:hp("2%") }} onPress={()=>{setModalVisible(!modalVisible);uploadData()}}>
                                    <Text style={{color:"white",fontFamily:"Quicksand-Bold",fontSize:16}}>Submit</Text>
                                </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </Modal>
        </Grid>);
}

