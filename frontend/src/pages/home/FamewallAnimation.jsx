import FamewallEmbed from "react-famewall";
import "./home.css";

const FamewallAnmation = () => {
  return (
    <div className="testimonials w-full h-full mt-12">
      <h1 className="text-center text-white text-[25px] md:text-[40px] font-bold mb-6">
        App Reviews and Feedback
      </h1>
      <FamewallEmbed
        wallUrl="test999"
        cardTheme="light"
        dualSliderMode={true}
      />
    </div>
  );
};

export default FamewallAnmation;
