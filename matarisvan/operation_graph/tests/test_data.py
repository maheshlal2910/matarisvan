user_test_data = [ {
    "name" : "John Doe",
    "level" : {
      "name" : "myTW User",
      "description" : "All users of myTW",
      "points" : 0,
      "resources" : {
        "image" : {
          "ref" : "https://images.your.domain.com/api/core/v2/images/status/c/statuslevel-1210.gif",
          "allowed" : [ "GET" ]
        }
      }
    },
    "username" : "johndoe",
    "email" : "johndoe@domain.com",
    "resources" : {
      "self" : {
        "ref" : "https://your.domain.com/api/core/v2/users/1278237",
        "allowed" : [ "GET" ]
      },
      "avatar" : {
        "ref" : "https://your.domain.com/api/core/v2/avatars/default",
        "allowed" : [ "GET" ]
      }
    },
    "id" : 1278237
  }, 
  {
    "name" : "Alice Bob",
    "level" : {
      "name" : "myTW User",
      "description" : "All users of myTW",
      "points" : 0,
      "resources" : {
        "image" : {
          "ref" : "https://your.domain.com/api/core/v2/images/status/c/statuslevel-902.gif",
          "allowed" : [ "GET" ]
        }
      }
    },
    "username" : "alicebob",
    "email" : "alicebob@domain.com",
    "resources" : {
      "self" : {
        "ref" : "https://your.domain.com/api/core/v2/users/67164",
        "allowed" : [ "GET" ]
      },
      "avatar" : {
        "ref" : "https://your.domain.com/api/core/v2/avatars/default",
        "allowed" : [ "GET" ]
      }
    },
    "id" : 67164
  } ]

discussion_data = {
    'message' : {'subject': 'subject is nothing'}
}
