import React from "react";
import HomeScreen from "../screens/Home";
import TopTabNav from "./topTabNav";
import LoginScreen from "../screens/LoginScreen";
import Logout from "../screens/Logout";
import RegisterScreen from "../screens/Register";
import { createStackNavigator } from "@react-navigation/stack";
import * as firebase from "firebase";
import { firebaseConfig } from "../config";


if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
} else {
  firebase.app();
}

const AppStackNavigation = createStackNavigator();
export default function StackNav() {
  return (
    <AppStackNavigation.Navigator
      initialRouteName="Login"  screenOptions={{
        headerShown: false,
        }}>
    

      <AppStackNavigation.Screen name="Login" component={LoginScreen} />
       
      <AppStackNavigation.Screen name="RegisterScreen" component={RegisterScreen} />
      <AppStackNavigation.Screen name="Home" component={HomeScreen} />
      <AppStackNavigation.Screen name="Movies" component={TopTabNav} />
    </AppStackNavigation.Navigator>
    
  );
}
