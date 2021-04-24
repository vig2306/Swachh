import React, { useState, useEffect } from "react";
import Colors from '../constants/colors';
import { StyleSheet, Text, View, Image, TextInput, CheckBox, TouchableOpacity, StatusBar } from 'react-native';
import { Dimensions } from 'react-native'
import { FontAwesome5 } from '@expo/vector-icons';
import axios from "axios";
import Constants from '../constants/text';
export default function ResetPassword({ navigation }) {
    const [dataLoaded, setDataLoaded] = useState(false);
    const [phone, onChangephone] = useState('');
    const [email, onChangeemail] = useState('');
    const [name, onChangeName] = useState('');
    const [password, onChangePassword] = useState('');
    const [vr_password, onChangeVr_Password] = useState('');
    const [rememberMe, setrememberMe] = useState(false);
    const [otp, setotp] = useState(false);

    const handleClick = () => setrememberMe(!rememberMe)

    const reset = async () => {
        try {
            // Keep on showing the SlashScreen
            const data = {
                "otp":otp,
                "user_password": password,
                "vr_password": vr_password
            }
            axios
                .post(`${Constants.ApiLink}/api/reset`, data)
                .then(async function (response) {
                    // handle success

                    try {
                        const jsonValue = JSON.stringify(response.data);
                        // await AsyncStorage.setItem("userData", jsonValue);
                        console.log("data: " + jsonValue);
                        console.log("1");
                        navigation.navigate('Home');
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
           


            console.log(name, phone, password);
            navigation.navigate('Home')
        } catch (e) {
            console.warn(e);
        } finally {
            setDataLoaded(true);
            // Hiding the SplashScreen

        }
    }



    return (
        <View style={styles.container}>
            <View style={{ flexDirection: "row" }}>
                <Image source={require('../assets/images/logo.png')} style={styles.logo} />
            </View>
            <Text style={styles.tagline}>Reset Password</Text>
            <View style={styles.form}>
                <TextInput
                    style={styles.formInputs}
                    placeholder="OTP"
                    placeholderTextColor="#95a5a6"
                    onChangeText={text => setotp(text)}
                    value={otp}
                />
                <TextInput
                    style={styles.formInputs}
                    placeholder="Your password"
                    placeholderTextColor="#95a5a6"
                    onChangeText={text => onChangePassword(text)}
                    value={password}
                    secureTextEntry={true}
                />
                <TextInput
                    style={styles.formInputs}
                    placeholder="Verify your Password"
                    placeholderTextColor="#95a5a6"
                    onChangeText={text => onChangeVr_Password(text)}
                    value={vr_password}
                    secureTextEntry={true}
                />
                <TouchableOpacity style={styles.formButton} onPress={reset}>
                    <View style={{ backgroundColor: "black", padding: "4%", borderRadius: 10 }}>
                        <FontAwesome5 name="arrow-right" size={20} color="white" />
                    </View>
                    <View style={{ padding: "4%", }}>
                        <Text style={{ fontFamily: "Quicksand-Bold", fontSize: Dimensions.get('window').height / 40 }}>  Reset</Text>
                    </View>
                </TouchableOpacity>
            </View>
        </View>
    );
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        paddingHorizontal: '6%',
        justifyContent: 'center',
        marginTop: StatusBar.currentHeight
    },
    logo: {
        height: Dimensions.get('window').height / 4,
        width: Dimensions.get('window').width / 1.6,
        alignSelf: 'flex-start',
        marginBottom: '8%'
    },
    tagline: {
        fontFamily: "Quicksand-Bold",
        fontSize: Dimensions.get('window').width / 12,
    },
    form: {
        paddingTop: "6%"
    },
    formInputs: {
        height: Dimensions.get('window').height / 14,
        borderRadius: 10,
        backgroundColor: "#ecf0f1",
        fontFamily: "Quicksand-SemiBold",
        paddingHorizontal: "5%",
        marginVertical: "2%",
        fontSize: Dimensions.get('window').height / 42,
        color: "#34495e"
    },
    formButton: {
        flexDirection: 'row',
        alignContent: "center",
        alignItems: "center",
        marginVertical: "4%"

    },
    checkbox: {
        alignSelf: "center",
        borderRadius: 10,

    },
    rememberMe: {
        flexDirection: "row",
        alignItems: "center",
        marginVertical: "4%",

    },
    rememberMeLabel: {
        fontFamily: "Quicksand-SemiBold",
        fontSize: Dimensions.get('window').height / 45,
    },
    labels: {
        fontFamily: "Quicksand-SemiBold",
        fontSize: Dimensions.get('window').height / 44,

    },
    textButtonsContainer: {
        paddingRight: "2%",
        justifyContent: "flex-end",
        marginVertical: "6%",
        paddingBottom: "5%"
    },
    textButton: {
        color: Colors.primaryColor,
        fontFamily: "Quicksand-Bold",
        fontSize: Dimensions.get('window').height / 42,
    }
});