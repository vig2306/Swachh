import React, { useState, useEffect } from "react";
import Colors from '../constants/colors';
import { StyleSheet, Text, View, Image, TextInput, CheckBox, TouchableOpacity, StatusBar } from 'react-native';
import { Dimensions } from 'react-native'
import { FontAwesome5 } from '@expo/vector-icons';
import axios from "axios";
import AsyncStorage from "@react-native-community/async-storage";
import Constants from '../constants/text';
import * as Font from 'expo-font';

export default function ForgotPassword({ navigation }) {
    const [dataLoaded, setDataLoaded] = useState(false);
    const [email, onChangeemail] = useState('');
    const [password, onChangePassword] = useState('');
    const [rememberMe, setrememberMe] = useState(false);
    const handleClick = () => setrememberMe(!rememberMe)

    const forget = async () => {
        try {
            const data={
                "user_email": email,
            }
            axios
                .post(`${Constants.ApiLink}/api/forget`, data)
                .then(async function (response) {
                    // handle success

                    try {
                        const jsonValue = JSON.stringify(response.data);
                        await AsyncStorage.setItem("userData", jsonValue);
                        console.log("data: " + jsonValue);
                        console.log("1");
                        navigation.navigate('ResetPassword');
                        //if else daalna hai
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
           
            // await fetchFonts();
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
                    placeholder="Your email"
                    placeholderTextColor="#95a5a6"
                    onChangeText={text => onChangeemail(text)}
                    value={email}
                />
                <TouchableOpacity style={styles.formButton} onPress={forget}>
                    <View style={{ backgroundColor: "black", padding: "4%", borderRadius: 10 }}>
                        <FontAwesome5 name="arrow-right" size={20} color="white" />
                    </View>
                    <View style={{ padding: "4%", }}>
                        <Text style={{ fontFamily: "Quicksand-Bold", fontSize: Dimensions.get('window').height / 40 }}>  Send Email</Text>
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
        justifyContent: 'center'
    },
    logo: {
        height: Dimensions.get('window').height / 4,
        width: Dimensions.get('window').width / 1.6,
        alignSelf: 'flex-start',
        marginBottom: '8%'
    },
    tagline: {
        fontFamily: "Quicksand-Bold",
        fontSize: Dimensions.get('window').width / 10,
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