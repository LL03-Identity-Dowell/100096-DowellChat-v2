import React from "react";


const ProfileAvatar = ({
  fullName,
  profilePhotoUrl,
}) => {
  const placeholder = fullName
    .split(" ")
    .map((name) => name.charAt(0))
    .slice(0, 2)
    .join("");

  //To get the background color of the avatar based on the user's name
  const getBackgroundColor = () => {
    const asciiSum = fullName
      .split("")
      .reduce((sum, char) => sum + char.charCodeAt(0), 0);

    const r = (asciiSum * 37) % 255;
    const g = (asciiSum * 79) % 255;
    const b = (asciiSum * 127) % 255;
    return `rgb(${r}, ${g}, ${b})`;
  };

  const bgColor = getBackgroundColor();

  return (
    <div>
      {profilePhotoUrl ? (
        <img
          width={100}
          height={100}
          className="w-10 h-10 rounded-full object-cover"
          src={profilePhotoUrl || ""}
          alt={`${fullName} ProfilePicture`}
          title={fullName}
        />
      ) : (
        <div
          style={{ backgroundColor: bgColor }}
          className="bg-gray-300 cursor-pointer w-10 h-10 flex items-center justify-center rounded-full"
          title={fullName}
        >
          <span className="text-white text-lg">{placeholder}</span>
        </div>
      )}
    </div>
  );
};
export default ProfileAvatar;