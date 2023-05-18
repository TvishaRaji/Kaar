import { Injectable } from '@angular/core';
import {Auth, signInWithEmailAndPassword, signOut } from '@angular/fire/auth'
import { from } from 'rxjs';
import {AngularFireAuth} from '@angular/fire/compat/auth'
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

//   constructor(private fireauth: AngularFireAuth, private router:Router) { }
//   login( email: string, password: string){
//     this.fireauth.signInWithEmailAndPassword(email, password).then(() =>{
//       localStorage.setItem('token','true');
//       this.router.navigate(['home'])
//     },err => {
//       alert("idk man");
//       this.router.navigate(['/login'])
//     })
//   }

//   register(email:string, password:string){
//     this.fireauth.createUserWithEmailAndPassword(email,password).then(() => {
//       alert('Registeration successful');
//       this.router.navigate(['/login']);
//     }, (err) =>{
//       alert(err.message);
//       this.router.navigate(['/register'])
//     })
//   }

//   // logout(){
//   //   return from(this.auth.signOut());
//   // }
// logout(){
//   this.fireauth.signOut().then(() =>{
//     localStorage.removeItem('token');
//     this.router.navigate(['/login'])
//   }, err =>{
//     alert(err.message);
//   })
// }

constructor(private auth:Auth ){}
login(email: string, password: string){
  return from(signInWithEmailAndPassword(this.auth, email, password))
}
logout(){
    return from(this.auth.signOut());
 }
}

