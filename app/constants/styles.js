import { StyleSheet, Dimensions } from 'react-native';

const { width: winWidth, height: winHeight } = Dimensions.get('window');
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';

export default StyleSheet.create({
    preview: {
        height: winHeight,
        width: winWidth,
        position: 'absolute',
        left: 0,
        top: 0,
        right: 0,
        bottom: 0,
    },
    alignCenter: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    bottomToolbar: {
        width: winWidth,
        position: 'absolute',
        height: 100,
        bottom: 0,
    },
    captureBtn: {
        width: 60,
        height: 60,
        borderWidth: 2,
        borderRadius: 60,
        borderColor: "#FFFFFF",
    },
    captureBtnActive: {
        width: 80,
        height: 80,
    },
    captureBtnInternal: {
        width: 76,
        height: 76,
        borderWidth: 2,
        borderRadius: 76,
        backgroundColor: "white",
        borderColor: "transparent",
    },
    centeredView: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: 'rgba(0,0,0,0.7)',
    },
    modalView: {
        backgroundColor: "white",
        borderRadius: 20,
        padding: wp("3.5%"),
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 2
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
        width: wp("80%"),
        height: hp("28%")
    },
    openButton: {
        justifyContent: "center",
        marginLeft: "auto",
        borderRadius: 20,
        padding: wp("2%"),
        elevation: 2
    },
    formInputs: {
        height: hp("6%"),
        borderRadius: 5,
        backgroundColor: "#ecf0f1",
        fontFamily: "Quicksand-regular",
        paddingHorizontal: wp("4%"),
        marginVertical: hp("0.5%"),
        fontSize: wp('4%'),
        color: "#34495e"
    },
    modalHeader: {
        fontFamily: "Quicksand-medium",
        fontSize: wp('4.2%'),
        marginBottom: hp("1%")
    },
    fontStyle: {
        fontFamily: "Quicksand-Bold",
        fontSize: wp('4%')
    }

});
