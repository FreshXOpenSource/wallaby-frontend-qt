function(doc, req) {
  if((doc._id  != 'WallabyApp2' && doc._id != 'credentials' &&  "_design/" !== doc._id.substr(0, 8)) || doc.deleted) {
      return true;
  } else {
      return false;
  }  
}
